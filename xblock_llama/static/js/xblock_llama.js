$(function () {
    $('#get-response').click(function () {
        var prompt = $('#prompt').val();
        var modelType = $('#model-type').val(); // 获取选择的模型类型
        $.ajax({
            type: "POST",
            url: "/xblock/llama/handler/get_response",
            data: JSON.stringify({ 'prompt': prompt, 'model_type': modelType }), // 添加 model_type
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                var html = parseMarkdown(data.response); // 使用 Markdown 解析器
                $('#response').html(html);
            },
            error: function (error) {
                console.error("Error:", error);
                $('#response').text("Error: Could not get response.");
            }
        });
    });

    function parseMarkdown(markdown) {
        // 替换换行符为 <br> 标签
        markdown = markdown.replace(/\n/g, '<br>');

        // 匹配标题
        markdown = markdown.replace(/^# (.*)$/gm, '<h1>$1</h1>');
        markdown = markdown.replace(/^## (.*)$/gm, '<h2>$1</h2>');
        markdown = markdown.replace(/^### (.*)$/gm, '<h3>$1</h3>');
        markdown = markdown.replace(/^#### (.*)$/gm, '<h4>$1</h4>');
        markdown = markdown.replace(/^##### (.*)$/gm, '<h5>$1</h5>');
        markdown = markdown.replace(/^###### (.*)$/gm, '<h6>$1</h6>');

        // 匹配粗体和斜体
        markdown = markdown.replace(/\*\*(.*)\*\*/g, '<b>$1</b>');
        markdown = markdown.replace(/\*(.*)\*/g, '<i>$1</i>');

        // 匹配删除线
        markdown = markdown.replace(/~~(.*)~~/g, '<del>$1</del>');

        // 匹配链接
        markdown = markdown.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');

        // 匹配图片
        markdown = markdown.replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1">');

        // 匹配列表
        markdown = markdown.replace(/^(\*|\-) (.*)$/gm, '<ul><li>$2</li></ul>');
        markdown = markdown.replace(/^(\d+)\. (.*)$/gm, '<ol><li>$2</li></ol>');

        // 匹配引用
        markdown = markdown.replace(/^> (.*)$/gm, '<blockquote>$1</blockquote>');

        // 匹配代码块
        markdown = markdown.replace(/`(.*?)`/gs, '<pre><code>$1</code></pre>');

        // 匹配行内代码
        markdown = markdown.replace(/`(.*?)`/g, '<code>$1</code>');

        return markdown;
    }
});