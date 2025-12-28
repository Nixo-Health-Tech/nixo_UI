(function(){
  var messagesEl = document.getElementById('messages');
  var input = document.getElementById('message');
  var sendBtn = document.getElementById('send');
  var stopBtn = document.getElementById('stop');
  var modelSel = document.getElementById('model');
  var ragSel = document.getElementById('use_rag');
  var es = null;
  function append(role, text) {
    var wrap = document.createElement('div');
    wrap.className = 'msg ' + role;
    var who = document.createElement('strong');
    who.textContent = (role === 'user') ? 'شما: ' : 'دستیار: ';
    var span = document.createElement('span');
    span.textContent = text || '';
    wrap.appendChild(who); wrap.appendChild(span);
    messagesEl.appendChild(wrap);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return span;
  }
  function startStream(q) {
    if (!q) return;
    sendBtn.disabled = true;
    var model = (modelSel && modelSel.value) ? modelSel.value : '';
    var disableRag = (ragSel && ragSel.value === 'off') ? '1' : '';
    append('user', q);
    var span = append('assistant', '');
    var params = new URLSearchParams();
    params.set('message', q);
    if (model) params.set('model', model);
    if (disableRag) params.set('disable_rag', '1');
    var url = '/chat/handler/?' + params.toString();
    es = new EventSource(url);
    es.onmessage = function(ev){
      try {
        var data = JSON.parse(ev.data);
        if (data.token) { span.textContent += data.token; }
        if (data.error) { span.textContent += '\n[خطا] ' + data.error; }
      } catch(e){}
    };
    es.addEventListener('end', function(){ stopStream(); });
    es.onerror = function(){ stopStream(); };
  }
  function stopStream(){
    if (es) { es.close(); es = null; }
    sendBtn.disabled = false;
  }
  sendBtn.addEventListener('click', function(){
    var q = (input.value || '').trim();
    if (!q) return;
    startStream(q);
    input.value = ''; input.focus();
  });
  input.addEventListener('keydown', function(e){
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      var q = (input.value || '').trim();
      if (!q) return;
      startStream(q);
      input.value = '';
    }
  });
  stopBtn.addEventListener('click', stopStream);
})();
