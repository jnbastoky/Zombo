# Zombo Site

## Create Site

Create temporary `Docker` container
```bash
docker build -t hugo .
docker run -it --rm -p 1313:1313 -v ./:/app hugo bash
```

In the container
```bash
cd /app
hugo new site --force .
hugo mod init github.com/jnbastoky/Zombo
```

Create `onfig/_default/module.toml`:
```toml
[[imports]]
path = "github.com/jpanther/congo/v2"
```

Test Server
```bash
hugo server --bind=0.0.0.0
```

## Config files
```bash
rm hugo.toml
```

Copy config files from repo `config/_default` except `module.toml`


## Customize
https://jpanther.github.io/congo/docs/getting-started/