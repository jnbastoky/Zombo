# Zombo Site

## Create Site

Create [orphan branch](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/creating-a-github-pages-site-with-jekyll)

```bash
git checkout --orphan hugo
git rm -rf .
rm -rf ./*
```

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
hugo server --bind=0.0.0.0 -D
```

## Config files

```bash
rm hugo.toml
```

Copy config files from repo `config/_default` except `module.toml`

## Customize

[Congo Getting Started Guide](https://jpanther.github.io/congo/docs/getting-started/)

## Commit

```bash
git add .
git commit -m 'Initial hugo app'
git remote add origin https://github.com/jnbastoky/Zombo.git
git push -u origin hugo
```

## Adding Posts

```bash
hugo new content posts/YYYY-MM-DD-Title/index.md
```
