document.getElementById('formulario-calorias').addEventListener('submit', function(event) {
    let isValid = true;
    const errorMessage = document.getElementById('error');
    const inputGroups = document.querySelectorAll('.apartado, .apartadoSelecion');

    // Ocultar mensaje de error y restablecer colores
    errorMessage.style.display = 'none';
    inputGroups.forEach(group => {
        const inputs = group.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.style.borderColor = '';
            if (input.type === 'radio') {
                const label = document.querySelector(`label[for="${input.id}"]`);
                label.style.color = '';
            }
        });
    });

    // Verificar cada grupo de entrada
    inputGroups.forEach(group => {
        let groupValid;
        const inputs = group.querySelectorAll('input, select');

        if (group.classList.contains('apartado')) {
            groupValid = Array.from(inputs).every(input => input.value.trim() !== '');
        } else {
            groupValid = Array.from(inputs).some(input => input.checked);
            if (!groupValid) {
                inputs.forEach(input => {
                    if (!input.checked) {
                        const label = document.querySelector(`label[for="${input.id}"]`);
                        label.style.color = 'red';
                    }
                });
            }
        }

        if (!groupValid) {
            isValid = false;
            inputs.forEach(input => {
                if (input.value.trim() === '') {
                    input.style.borderColor = 'red';
                }
            });
        }
    });

    if (!isValid) {
        event.preventDefault(); // Evitar enviar el formulario
        errorMessage.style.display = 'block';
    }
});

