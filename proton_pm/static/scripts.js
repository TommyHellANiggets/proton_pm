function toggleSidebar() {
    var sidebar = document.querySelector('.sidebar');
    var contentInner = document.querySelector('.content-inner');
    var expandIcon = document.querySelector('.toggle-btn i'); // Обновленная строка

    // Изменяем иконку и ширину сайдбара в зависимости от состояния сайдбара
    if (sidebar.classList.contains('expanded')) {
        sidebar.classList.remove('expanded');
        sidebar.classList.add('collapsed');
        sidebar.style.width = '100px';
        contentInner.style.marginLeft = '100px'; // Смещаем контент вправо на 50 пикселей
        expandIcon.classList.remove('bi-x');
        expandIcon.classList.add('bi-justify');
    } else {
        sidebar.classList.remove('collapsed');
        sidebar.classList.add('expanded');
        sidebar.style.width = '300px';
        contentInner.style.marginLeft = '300px'; // Смещаем контент вправо на 350 пикселей
        expandIcon.classList.remove('bi-justify');
        expandIcon.classList.add('bi-x');
    }
}

document.addEventListener("DOMContentLoaded", function() {
    // Находим кнопку "Сохранить"
    const saveButton = document.querySelector(".save.submit");

    // Находим скрытую кнопку "submitBtn"
    const submitButton = document.getElementById("submitBtn");

    // Добавляем обработчик события на кнопку "Сохранить"
    saveButton.addEventListener("click", function() {
        // Программно вызываем клик на скрытой кнопке
        submitButton.click();
    });
});


// Инициализация массива для хранения файлов для предварительного просмотра
// Инициализация массива для хранения файлов для предварительного просмотра
let previewFiles = [];

// Функция для добавления файлов и обновления предварительного просмотра
function addFiles(event) {
    const fileInput = event.target;
    const files = Array.from(fileInput.files);

    // Объединяем файлы из input с существующими файлами в previewFiles
    const newFiles = files.filter(file => {
        // Проверяем, есть ли файл уже в previewFiles
        const existingFileIndex = previewFiles.findIndex(
            f => f.name === file.name && f.size === file.size
        );

        // Если файл не найден, добавляем его
        return existingFileIndex === -1;
    });

    // Добавляем новые файлы в массив previewFiles
    previewFiles = previewFiles.concat(newFiles);

    // Убеждаемся, что количество файлов не превышает 3
    if (previewFiles.length > 3) {
        previewFiles = previewFiles.slice(0, 3);
    }

    // Обновляем предварительный просмотр
    updatePreview();

    // Обновляем содержимое fileInput
    updateFileInput();
}

// Функция для обновления предварительного просмотра
function updatePreview() {
    const previewDiv = document.getElementById("filePreview");

    // Очистка предварительного просмотра
    previewDiv.innerHTML = "";

    // Отображение файлов из previewFiles
    previewFiles.forEach((file, index) => {
        const reader = new FileReader();

        reader.onload = (event) => {
            // Создаем контейнер для изображения и кнопки удаления
            const wrapper = document.createElement("div");
            wrapper.style.display = "inline-block";
            wrapper.style.position = "relative";
            wrapper.style.width = "170px";
            wrapper.style.height = "170px";

            // Создаем изображение
            const img = document.createElement("img");
            img.src = event.target.result;
            img.style.width = "170px";
            img.style.height = "170px";
            img.style.objectFit = "contain";

            // Создаем кнопку удаления
            const removeButton = document.createElement("button");
            removeButton.innerHTML = `
                <svg width="25" height="25" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <g clip-path="url(#clip0_1_248)">
                        <path d="M4.97648 5.29549C0.997431 9.45068 1.14021 16.0444 5.29541 20.0234C9.4506 24.0025 16.0443 23.8597 20.0233 19.7045C24.0024 15.5493 23.8596 8.95561 19.7044 4.97656C15.5492 0.997515 8.95553 1.1403 4.97648 5.29549ZM16.8545 9.45873L13.9727 12.4681L16.9821 15.3499L15.5412 16.8546L12.5318 13.9728L9.65 16.9822L8.14532 15.5413L11.0271 12.5319L8.01775 9.65009L9.45865 8.1454L12.468 11.0272L15.3498 8.01783L16.8545 9.45873Z" fill="#8A8A8A"/>
                    </g>
                    <defs>
                        <clipPath id="clip0_1_248">
                            <rect width="25" height="25" fill="white"/>
                        </clipPath>
                    </defs>
                </svg>`;

            // Стиль кнопки удаления
            removeButton.style.position = "absolute";
            removeButton.style.top = "0";
            removeButton.style.right = "0";
            removeButton.style.backgroundColor = "transparent";
            removeButton.style.border = "none";
            removeButton.style.cursor = "pointer";

            // Обработчик удаления файла
            removeButton.addEventListener("click", () => {
                // Удаляем файл из previewFiles
                previewFiles.splice(index, 1);

                // Обновляем предварительный просмотр и fileInput
                updatePreview();
                updateFileInput();
            });

            // Добавляем изображение и кнопку удаления в контейнер
            wrapper.appendChild(removeButton);
            wrapper.appendChild(img);

            // Добавляем контейнер в предварительный просмотр
            previewDiv.appendChild(wrapper);
        };

        reader.readAsDataURL(file);
    });
}

// Функция для обновления содержимого fileInput
function updateFileInput() {
    const fileInput = document.getElementById("formFileMultiple");
    const dataTransfer = new DataTransfer();

    // Добавляем файлы из previewFiles в dataTransfer
    previewFiles.forEach(file => dataTransfer.items.add(file));

    // Устанавливаем значение fileInput.files
    fileInput.files = dataTransfer.files;
}

// Привязываем обработчик к событию изменения input
document.getElementById("formFileMultiple").addEventListener("change", addFiles);


        // Получаем элементы кнопки и раскрывающегося содержимого
        const addSectionBtn = document.getElementById('addSectionBtn');
        const expandableContent = document.getElementById('expandableContent');

        // Добавляем обработчик события для кнопки
        addSectionBtn.addEventListener('click', function () {
            // Переключаем класс для раскрывающегося содержимого
            expandableContent.classList.toggle('active');
        });

    // Получаем кнопки
    const saveButton = document.querySelector('.cansel');
    const submitButton = document.getElementById('submitBtn');

    // Добавляем обработчик события на кнопку "Сохранить"
    saveButton.addEventListener('click', function() {
        // Когда нажимаем на "Сохранить", симулируем нажатие на кнопку отправки формы
        submitButton.click();
    });

document.addEventListener("DOMContentLoaded", function() {
    // Получаем кнопки
    const cancelButton = document.querySelector('.save');
    const resetButton = document.getElementById('formResetBtn'); // Изменено на 'formResetBtn'
    const form = document.getElementById('uploadForm');

    // Добавляем обработчик события на кнопку "Отмена"
    cancelButton.addEventListener('click', function() {
        // Очищаем значения формы
        form.reset();
    });

    // Добавляем обработчик события на кнопку "Сбросить"
    resetButton.addEventListener('click', function() {
        // Очищаем значения формы
        form.reset();
    });
});


// Обработчик нажатия на карандаш рядом с заголовком раздела
$('.edit-parent').click(function(e) {
    e.preventDefault();
    // Получаем значение content_id и title
    var content_id = $(this).data('id');
    var title = $(this).data('title');
    // Устанавливаем значение content_id в скрытое поле
    $('#content-id').val(content_id);
    // Устанавливаем значение title в текстовое поле
    $('#body').val(title);
    // Очищаем значения путей к изображениям
    $('input[name="image1"]').val('');
    $('input[name="image2"]').val('');
    $('input[name="image3"]').val('');
});

// Обработчик отправки формы редактирования контента
$('#edit-content-form').submit(function(e) {
    e.preventDefault();
    // Получаем данные формы
    var formData = new FormData(this);
    // Отправляем POST запрос
    $.ajax({
        url: '/edit_content/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            console.log(data);
            // Здесь можно выполнить какие-то действия после успешного сохранения
        },
        error: function(xhr, status, error) {
            console.error(error);
            // Здесь можно выполнить какие-то действия в случае ошибки
        }
    });
});
