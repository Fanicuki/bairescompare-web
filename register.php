<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registrarse</title>
</head>
<body>
    <h2>Registrarse</h2>
    <form action="register.php" method="post">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" name="nombre" required><br><br>
        <label for="apellido">Apellido:</label>
        <input type="text" id="apellido" name="apellido" required><br><br>
        <label for="usuario">Usuario:</label>
        <input type="text" id="usuario" name="usuario" required><br><br>
        <label for="contraseña">Contraseña:</label>
        <input type="password" id="contraseña" name="contraseña" required><br><br>
        <button type="submit">Registrarse</button>
    </form>
</body>
</html>

<?php
include 'db.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = $_POST['nombre'];
    $apellido = $_POST['apellido'];
    $usuario = $_POST['usuario'];
    $contraseña = $_POST['contraseña'];

    $contraseña_encriptada = password_hash($contraseña, PASSWORD_DEFAULT);

    $sql = "INSERT INTO Usuarios (nombre, apellido, usuario, contraseña) VALUES (?, ?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ssss", $nombre, $apellido, $usuario, $contraseña_encriptada);

    if ($stmt->execute()) {
        echo "Usuario registrado correctamente.";
    } else {
        echo "Error al registrar usuario: " . $stmt->error;
    }

    $stmt->close();
}

$conn->close();
?>
