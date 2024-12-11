from flask import Flask, render_template, request, jsonify
from .models import db, File
import boto3
import os

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('PGSQL_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bucket_region = os.getenv('AWS_DEFAULT_REGION')
bucket_name = os.getenv('AWS_BUCKET_NAME')
bucket_domain = os.getenv('BUCKET_DOMAIN', ' ')

db.init_app(app)

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=bucket_region
)

final_url = ''
    
with app.app_context():
    db.create_all()  # Create tables if they don't exist

@app.route('/')
def index():
    # Fetch files from the database
    page = int(request.args.get('page', 1))
    files_per_page = 60
    files = File.query.paginate(page=page, per_page=files_per_page)

    return render_template('index.html', files=files.items, page=files.page, total_pages=files.pages)

@app.route('/api/files', methods=['GET'])
def get_files():
    """
    API endpoint to fetch paginated file metadata.
    """
    # Get page number from query parameters (default to 1)
    page = int(request.args.get('page', 1))
    files_per_page = 60

    # Fetch paginated results from the database
    paginated_files = File.query.paginate(page=page, per_page=files_per_page)

    # Structure the response data
    response_data = {
        'files': [
            {
                'id': file.id,
                'key': file.key,
                'size': file.size,
                'file_type': file.file_type,
                'url': file.url,
            }
            for file in paginated_files.items
        ],
        'current_page': paginated_files.page,
        'total_pages': paginated_files.pages,
        'total_files': paginated_files.total,
    }

    return jsonify(response_data)
@app.route('/sync-files')
def sync_files():
    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' in response:
        for file in response['Contents']:
            # Check if the file already exists in the database
            if not File.query.filter_by(key=file['Key']).first():
                # Insert the file into the database
                new_file = File(
                    key=file['Key'],
                    size=file['Size'],
                    file_type=file['Key'].split('.')[-1],  # Extract file type from extension
                    url = f'https://{bucket_name}/{file["Key"]}' if bucket_name == bucket_domain else f'https://s3.{bucket_region}.amazonaws.com/{bucket_name}/{file["Key"]}'
                )
                db.session.add(new_file)
        db.session.commit()

    return 'Files synced successfully!'

if __name__ == '__main__':
    app.run(debug=True)
