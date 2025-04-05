function updateLineNumbers() {
    const editor = document.getElementById('json-editor');
    const lineNumbers = document.getElementById('line-numbers');
    
    // Calculate number of lines
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

function initEditor(errorData = {}) {
    const editor = document.getElementById('json-editor');
    const lineNumbers = document.getElementById('line-numbers');
    
    // Store error data in global scope
    window.errorData = errorData;
    
    // Initial update
    updateLineNumbers();
    
    // Update on scroll
    editor.addEventListener('scroll', updateLineNumbers);
    
    // Update on input
    editor.addEventListener('input', function() {
        updateLineNumbers();
    });
    
    // Highlight error if exists
    if (errorData?.error_pos !== null && errorData?.error_pos >= 0) {
        editor.focus();
        editor.setSelectionRange(errorData.error_pos, errorData.error_pos);
        
        // Scroll to error position
        const lineHeight = parseInt(getComputedStyle(editor).lineHeight);
        const lines = editor.value.substr(0, errorData.error_pos).split('\n');
        const lineNumber = lines.length - 1;
        editor.scrollTop = (lineNumber - 3) * lineHeight;
    }
}