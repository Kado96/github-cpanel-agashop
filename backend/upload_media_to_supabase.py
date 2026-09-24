import os
import glob
import boto3

endpoint = 'https://plihtjkucujoeewlzptb.storage.supabase.co/storage/v1/s3'
key_id = 'a71032320e2c3943422999eb064131b4'
secret = '6dc8ebb6645090e8829ef61054600730be17c59138be5572c8703c107da87cb1'

s3 = boto3.client(
    's3',
    endpoint_url=endpoint,
    aws_access_key_id=key_id,
    aws_secret_access_key=secret,
    region_name='eu-west-1'
)

media_dir = r'E:\Application\jarvis-starter-kit\deliverables\application\github-cpanel-agashop\backend\media'
files = [f for f in glob.glob(os.path.join(media_dir, '**', '*.*'), recursive=True) if os.path.isfile(f)]

print(f"Trouvé {len(files)} médias locaux. Début du transfert vers le bucket Supabase 'media'...")

success_count = 0
for f in files:
    rel_path = os.path.relpath(f, media_dir).replace('\\', '/')
    key = f"shops/global/{rel_path}"
    with open(f, 'rb') as file_data:
        try:
            s3.put_object(Bucket='media', Key=key, Body=file_data.read())
            success_count += 1
            print(f"[{success_count}/{len(files)}] Transfert réussi : {rel_path} -> {key}")
        except Exception as e:
            print(f"Erreur sur {rel_path}: {e}")

print(f"\n🎉 Migration terminée : {success_count}/{len(files)} fichiers migrés avec succès vers Supabase Storage S3 !")
