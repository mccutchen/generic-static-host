server {
    server_name wrm.io;

    root /var/www/wrm.io;
    index index.html index.php;

    location ~ /\.ht {
        deny all;
    }
}
