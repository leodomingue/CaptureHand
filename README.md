# CaptureHand

Proyecto para captura y visualización de manos

## 1. Clona el repositorio:
```bash
git clone https://github.com/leodomingue/CaptureHand.git
cd CaptureHand
pip install -r requirements.txt
```

## 2. Ejecuta la app
```bash
python main.py
```

## 3. Opcionalmente create un environment


## 4. Si quieren contribuir al repo lo recomendado es crear su branch y luego hacer pull request

En su terminal escriben:
```bash
#1. para crear y cambiar a su branch
git checkout -b nombre-de-su-branch 

#2. Agregar cambios y hacer commit
git add .
git commit -m "commit (nombre): hago tal cosa"

#3. Subir branch 
git push -u origin nombre-de-su-branch
```

Luego en GitHub van a **Pull Requests** y la mandan a `master`.

Luego si quieren volver al branch
```bash
# 1. Actualizar main local
git checkout master
git pull origin master

# 2. Volver a tu branch de trabajo
git checkout nombre-de-su-branch

# 3. Actualizar tu branch con los últimos cambios de main
git merge master
```
