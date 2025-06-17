document.addEventListener('DOMContentLoaded', function () {
        const slider = document.getElementById('slider');
        const sliderValue = document.getElementById('sliderValue');

        // Atualiza o valor inicial
        sliderValue.textContent = slider.value;

        // Atualiza em tempo real conforme o slider é movido
        slider.addEventListener('input', function () {
            sliderValue.textContent = this.value;
        });
    });

document.addEventListener('DOMContentLoaded', function () {
        const senhaEl = document.getElementById('senha');
        const copiarBtn = document.getElementById('copiarBtn-Senha');

        copiarBtn.addEventListener('click', function () {
            const senha = senhaEl.textContent.trim();

            // Cria um input temporário para copiar a senha
            const tempInput = document.createElement('input');
            tempInput.value = senha;
            document.body.appendChild(tempInput);
            tempInput.select();
            document.execCommand('copy');
            document.body.removeChild(tempInput);

            // Feedback visual (opcional)
            copiarBtn.textContent = "Copiado!";
            setTimeout(() => copiarBtn.textContent = "Copiar", 2000);
        });
    });

document.addEventListener('DOMContentLoaded', function () {
        const cpfEl = document.getElementById('cpf');
        const copiarBtn = document.getElementById('copiarBtn-CPF');

        copiarBtn.addEventListener('click', function () {
            const senha = cpfEl.textContent.trim();

            // Cria um input temporário para copiar o CPF
            const tempInput = document.createElement('input');
            tempInput.value = senha;
            document.body.appendChild(tempInput);
            tempInput.select();
            document.execCommand('copy');
            document.body.removeChild(tempInput);

            // Feedback visual (opcional)
            copiarBtn.textContent = "Copiado!";
            setTimeout(() => copiarBtn.textContent = "Copiar", 2000);
        });
    });

    