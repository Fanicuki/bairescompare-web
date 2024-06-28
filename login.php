<?php
include 'db.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $usuario = $_POST['usuario'];
    $contraseña = $_POST['contraseña'];

    $sql = "SELECT id, nombre, apellido, contraseña FROM Usuarios WHERE usuario = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $usuario);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        $stmt->bind_result($id, $nombre, $apellido, $contraseña_encriptada);
        $stmt->fetch();
        if (password_verify($contraseña, $contraseña_encriptada)) {
            header("Location: http://127.0.0.1:5000/");
        } else {
            echo "Usuario o contraseña incorrectos.";
        }
    } else {
        echo "Usuario no encontrado.";
    }

    $stmt->close();
}

$conn->close();
?>
