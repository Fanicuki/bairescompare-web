<?php
$contraseñas = ["contraseña1", "contraseña2", "contraseña3"];
foreach ($contraseñas as $contraseña) {
    echo password_hash($contraseña, PASSWORD_DEFAULT) . "\n";
}
?>
