// Función para guardar el valor del elemento <li> y devolverlo a Django
function seleccionarElemento(elemento) {
    document.getElementById('elemento_seleccionado').value = elemento;
    document.getElementById('formulario').submit();
}
