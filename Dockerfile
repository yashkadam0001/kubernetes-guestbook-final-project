FROM nginx:alpine

# Explicitly copy application HTML to Nginx web root
COPY index.html /usr/share/nginx/html/index.html

# Expose web server HTTP port
EXPOSE 80

# Start Nginx server in foreground
CMD ["nginx", "-g", "daemon off;"]
