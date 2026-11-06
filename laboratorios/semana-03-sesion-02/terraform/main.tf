terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.0"
    }
  }
}

provider "docker" {}

resource "docker_network" "red_taxis" {
  name = "red-taxis"
}

resource "docker_volume" "datos_postgres" {
  name = "datos-postgres"
}

resource "docker_image" "postgres" {
  name = "postgres:13"
}

resource "docker_image" "pgadmin" {
  name = "dpage/pgadmin4:9.18"
}

resource "docker_image" "ingesta" {
  name = "demo-taxis-ingesta:local"
  build {
    context = "${path.module}/../"
  }
}

resource "docker_container" "pg_database" {
  name  = "pg-database"
  image = docker_image.postgres.image_id

  env = [
    "POSTGRES_USER=taxi_user",
    "POSTGRES_PASSWORD=taxi_pass",
    "POSTGRES_DB=taxi_db",
  ]

  ports {
    internal = 5432
    external = 5432
  }

  volumes {
    volume_name    = docker_volume.datos_postgres.name
    container_path = "/var/lib/postgresql/data"
  }

  networks_advanced {
    name    = docker_network.red_taxis.name
    aliases = ["pg-database"]
  }
}

resource "docker_container" "pgadmin" {
  name  = "pgadmin"
  image = docker_image.pgadmin.image_id

  env = [
    "PGADMIN_DEFAULT_EMAIL=admin@example.com",
    "PGADMIN_DEFAULT_PASSWORD=admin123",
  ]

  ports {
    internal = 80
    external = 8085
  }

  networks_advanced {
    name = docker_network.red_taxis.name
  }

  depends_on = [docker_container.pg_database]
}

resource "docker_container" "ingesta" {
  name  = "ingesta"
  image = docker_image.ingesta.image_id

  # La ingesta carga los datos y termina. Sin esto, Terraform espera que el
  # contenedor siga corriendo y cada plan propone volver a arrancarlo.
  must_run = false

  env = [
    "PG_HOST=pg-database",
    "PG_PORT=5432",
    "PG_DATABASE=taxi_db",
    "PG_USER=taxi_user",
    "PG_PASSWORD=taxi_pass",
    "PG_TABLE=viajes_taxi",
  ]

  networks_advanced {
    name = docker_network.red_taxis.name
  }

  depends_on = [docker_container.pg_database]
}