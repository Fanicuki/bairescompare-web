<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar Sesión</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="bairescompare_icon.png" alt="">
        </div>
        <h2>Iniciar Sesión</h2>
        <form action="login.php" method="post">
            <label for="usuario">Usuario:</label>
            <input type="text" id="usuario" name="usuario" required>
            <label for="contraseña">Contraseña:</label>
            <input type="password" id="contraseña" name="contraseña" required>
            <button type="submit">Iniciar Sesión</button>
        </form>
        <hr class="dashed">
        <p>¿No tiene cuenta? <a href="register.php">Registrarse</a></p>
    </div>
</body>
</html>
