# Getting Started

### Install Docker

[Docker Installation Guide](https://docs.docker.com/engine/install/debian/)

tldr; run
```bash
sudo apt-get update
sudo apt-get install \
  ca-certificates \
  curl \
  gnupg \
  lsb-release

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

sudo docker run hello-world
```

### Install Docker Compose
[Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

tldr; run
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-linux-aarch64" -o /usr/local/bin/docker-compose #see note

sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version
```

Note: `uname -s`and `uname -m` outputs are weird on Raspberry Pis resulting in invalid download links. The default command from the guide does not work. Replace `uname -s` with linux and `uname -m` with aarch64.

### Git Clone and Run

Git clone
```bash
git clone https://github.com/lhr-solar/DataAcquisition
```
Make sure Docker Desktop is open then run it!

```bash
cd DataAcquisition #if you're not already in the directory
docker-compose up --build
```

### Grafana

Open localhost:3000, login, then navigate to the BPS dashboard.
