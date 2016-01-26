import gnupg

gpg = gnupg.GPG(gnupghome='./.gnupg')
input_data = gpg.gen_key_input(name_email="kroopeshkumar@yahoo.com", passphrase='my passphrase')

key = gpg.gen_key(input_data)
print key

open('./sync/my-unencrypted.txt', 'w').write('You need to Google Venn diagram.')
with open('./sync/my-unencrypted.txt', 'rb') as f:
    status = gpg.encrypt_file(
        f, recipients=['kroopeshkumar@yahoo.com'],
        output='sync/my-encrypted.txt')

print 'ok: ', status.ok
print 'status: ', status.status
print 'stderr: ', status.stderr

with open('sync/my-encrypted.txt', 'rb') as f:
    status = gpg.decrypt_file(f, passphrase='my passphrase', output='sync/my-decrypted.txt')

print 'ok: ', status.ok
print 'status: ', status.status
print 'stderr: ', status.stderr
