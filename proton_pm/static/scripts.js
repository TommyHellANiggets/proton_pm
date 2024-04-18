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
