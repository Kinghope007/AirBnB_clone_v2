# web_static_setup.pp

# Check if Nginx is installed and install it if not
exec { 'update':
  command => 'apt-get update',
  provider => shell,
}
-> exec { 'install':
  command => 'apt-get -y install nginx',
  provider => shell,
}

# Create necessary directories
-> exec { 'create_test_folder':
  command => 'mkdir -p /data/web_static/releases/test/',
  provider => shell,
}
-> exec { 'create_shared_folder':
  command => 'mkdir -p /data/web_static/shared/',
  provider => shell,
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  content => 'Fake content for testing',
}

# Create the symbolic link pointing to /data/web_static/releases/test/
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Update Nginx configuration
-> exec { 'permission':
  command => 'chown -R ubuntu:ubuntu /data/',
  provider => shell,
}
-> exec { 'add_lines':
  command => 'sudo sed -i "s|server_name _;|server_name _;\n\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}|" /etc/nginx/sites-enabled/default',
  provider => shell,
}

# restart nginx
-> exec { 'restart':
  command => 'sudo service nginx restart',
  provider => shell,
}
