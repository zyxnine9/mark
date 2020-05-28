 echo 密码是Health.pcl
# echo ssh engineer@47.112.232.246
#scp -r ./dist engineer@47.112.232.246:/home/engineer/zyx
npm run build
scp -r ./dist/* engineer@47.112.232.246:/data/webapps/mark-frontend/dist
