function initEditor(options = {}) {
    const editor = document.getElementById('json-editor');
    const lineNumbers = document.getElementById('line-numbers');
    
    // Сохраняем данные об ошибке в глобальной области
    if (options.error_line && options.error_pos) {
        window.errorData = {
            error_line: options.error_line,
            error_pos: options.error_pos
        };
    }

    function updateLineNumbers() {
        const lineHeight = parseInt(getComputedStyle(editor).lineHeight);
        const editorHeight = editor.clientHeight;
        const scrollTop = editor.scrollTop;
        const visibleLines = Math.ceil(editorHeight / lineHeight);
        
        // Get total lines
        const totalLines = editor.value.split('\n').length;
        
        // Calculate first visible line
        const firstVisibleLine = Math.floor(scrollTop / lineHeight) + 1;
        
        // Generate line numbers for visible area
        lineNumbers.innerHTML = '';
        for (let i = 0; i < visibleLines; i++) {
            const lineNumber = firstVisibleLine + i;
            if (lineNumber > totalLines) break;
            
            const lineElement = document.createElement('div');
            lineElement.textContent = lineNumber;
            
            // Highlight error line if it matches
            if (window.errorData?.error_line && lineNumber === window.errorData.error_line) {
                lineElement.style.fontWeight = 'bold';
                lineElement.style.color = '#d32f2f';
            }
            
            lineNumbers.appendChild(lineElement);
        }
        
        // Sync scroll positions
        lineNumbers.scrollTop = scrollTop;
    }

    // Добавляем обработчик для подсветки ошибки
    function highlightError() {
        if (window.errorData?.error_line && window.errorData?.error_pos) {
            const lines = editor.value.split('\n');
            if (window.errorData.error_line <= lines.length) {
                // Можно добавить подсветку текста ошибки здесь
                console.log('Error on line:', window.errorData.error_line);
            }
        }
    }

    // Инициализация
    editor.addEventListener('input', updateLineNumbers);
    editor.addEventListener('scroll', updateLineNumbers);
    
    // Вызываем при загрузке
    updateLineNumbers();
    highlightError();

    // Возвращаем функции, если нужно вызывать их извне
    return {
        updateLineNumbers,
        highlightError
    };
}