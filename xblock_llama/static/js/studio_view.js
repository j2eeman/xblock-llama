
function LlamaXBlockStudioView(runtime, element, context) {
    $('#save-display-name').click(function () {
        var display_name = $('#display_name').val();
        $('#save-status').text("Saving..."); // 显示保存状态

        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'save_display_name'),
            data: JSON.stringify({ 'display_name': display_name }),
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                if (data.success) {
                    $('#save-status').text("Saved!");
                } else {
                    $('#save-status').text("Error: " + data.message);
                }
            },
            error: function (error) {
                console.error("Error:", error);
                $('#save-status').text("Error: Could not save.");
            },
            complete: function () {
                setTimeout(function () { $('#save-status').text("") }, 3000); // 3秒后清除提示信息
            }
        });
    });

    $('#save-deepseek-api-key').click(function () {
        var deepseek_api_key = $('#deepseek_api_key').val();
        $('#save-deepseek-api-key-status').text("Saving...");

        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'save_deepseek_api_key'),
            data: JSON.stringify({ 'deepseek_api_key': deepseek_api_key }),
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                if (data.success) {
                    $('#save-deepseek-api-key-status').text("Saved!");
                } else {
                    $('#save-deepseek-api-key-status').text("Error: " + data.message);
                }
            },
            error: function (error) {
                console.error("Error:", error);
                $('#save-deepseek-api-key-status').text("Error: Could not save.");
            },
            complete: function () {
                setTimeout(function () { $('#save-deepseek-api-key-status').text("") }, 3000); // 3秒后清除提示信息
            }
        });
    });

    $('#save-model-type').click(function () {
        var modelType = $('#model_type').val();
        $('#save-model-type-status').text("Saving...");

        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'save_model_type'),
            data: JSON.stringify({ 'model_type': modelType }),
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                if (data.success) {
                    $('#save-model-type-status').text("Saved!");
                } else {
                    $('#save-model-type-status').text("Error: " + data.message);
                }
            },
            error: function (error) {
                console.error("Error:", error);
                $('#save-model-type-status').text("Error: Could not save.");
            },
            complete: function () {
                setTimeout(function () { $('#save-model-type-status').text("") }, 3000); // 3秒后清除提示信息
            }
        });
    });
}

function js_init_fn(runtime, element, context) {
    return new LlamaXBlockStudioView(runtime, element, context);
}

$(function () {
    runtime.register('LlamaXBlockStudioView', js_init_fn);
    // runtime.register('llama', js_init_fn);
});
