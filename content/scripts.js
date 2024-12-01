window.addEventListener('load', function() {
    window.MathJax = {
        tex: {
            inlineMath: [['\\$', '\\$'], ['\\(', '\\)']]
        }
    };
    hljs.highlightAll();
});
