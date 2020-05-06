import conducto as co

DOC = """\
This pipeline shows an example of connecting to an SSH server 
automatically."""

def sshtest() -> co.Serial:
    img = co.Image("debian")

    output = co.Serial(image=img, same_container=co.SameContainer.NEW, doc=DOC)
    output['config'] = co.Exec("""set -ex
if [ -z "$MY_ID_RSA" ]; then
    >&2 echo "You must set MY_ID_RSA secret or env"
    exit 1
fi  
apt-get update
apt-get install ssh -y
mkdir ~/.ssh
echo $MY_ID_RSA | base64 -d > ~/.ssh/id_rsa
chown 600 ~/.ssh/id_rsa
ssh-keyscan -H $MY_IP >> ~/.ssh/known_hosts
chown 600 ~/.ssh/known_hosts""")
    output["show-file"] = co.Exec("""ssh joel@$MY_IP ls -la""")

    return output

if __name__ == "__main__":
    co.main()
