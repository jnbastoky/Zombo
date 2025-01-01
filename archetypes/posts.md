+++
title = '{{ replace (.File.ContentBaseName | replaceRE "^\\d{4}-\\d{2}-\\d{2}-" "") "-" " " | title }}'
date = {{ .Date }}
draft = true
categories = [""]
tags = [""]
+++