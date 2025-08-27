import paramiko

def fetch_from_sftp():
    host = "172.16.180.86"
    port = 22
    username = "windF"
    password = "server8373"

    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    try:
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get("/home/OUTPUT/postproc_out/Sakoo_V01/gfs.2025082412/Sakoo_2025082504.pdf", "sakoofiletest.pdf")  # دانلود
        sftp.close()
        transport.close()
    except Exception as e:
        print(str(e))

# /home/OUTPUT/postproc_out/Sakoo_V01/gfs.2025082412
fetch_from_sftp()

# from django.http import FileResponse
# import paramiko
# import tempfile

# def download_file_view():
#     host = "172.16.180.86"
#     # port = 22
#     username = "windF"
#     password = "server8373"

#     remote_path = "home/OUTPUT/postproc_out/Sakoo_V01/Sakoo/gfs.2025082412/Sakoo_2025082504.pdf"

#     transport = paramiko.Transport((host, 22))
#     transport.connect(username=username, password=password)
#     sftp = paramiko.SFTPClient.from_transport(transport)

#     tmp = tempfile.NamedTemporaryFile(delete=False)
#     sftp.get(remote_path, tmp.name)
#     sftp.close()
#     transport.close()

    # return FileResponse(open(tmp.name, "rb"), as_attachment=True, filename="sakoofiletest.pdf")

# download_file_view()