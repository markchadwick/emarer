(function(jQuery) {
jQuery.fn.Task = function(settings, callback) {

    settings = jQuery.extend({
        local_id:   jQuery.uuid()
    }, settings);

    ////////////////////////////////////////////////////////////////////////////
    // Fields Vars
    var _input = []
    var _emitted = []
    

    ////////////////////////////////////////////////////////////////////////////
    // Private Methods

    function emit(key, value) {
        _emitted.push([key, value])
    }

    function _perform_map_task(data, map_func, combine_func) {
        _emitted = []
        jQuery.each(data.split('\n'), function(i, line) {
            map_func(null, line);
        });
        
        _flush_emitted();

    }
    
    function _flush_emitted() {
        var emit_values = new Object();
        var local_id    = settings.local_id;
        var action      = '/tasks/flush/' + settings.task_id;
        
        jQuery.each(_emitted, function(i, kv) {
            var key = kv[0];
            var val = kv[1];
            
            if(!emit_values[key]) {
                emit_values[key] = [val];
            } else {
                emit_values[key].push(val);
            }
        });
        
        jQuery.post(action, emit_values);
        _emitted = [];
    }

    function _compilation_error(type, error) {
        console.log(type, 'compilation error', error);
    }

    ////////////////////////////////////////////////////////////////////////////
    // Main
    
    function refetch() {
        settings.callback();
    }
    
    function main() {
        if(settings.task_type == 'map') {
            var mapper   = null;
            var combiner = null;

            try {
                eval("mapper = "+ settings.mapper);
            } catch(e) {
                _compilation_error('Mapper', e);
            }
            
            try {
                eval("combiner = "+ settings.combiner);
            } catch(e) {
                _compilation_error('Combiner', e);
            }
            
            _perform_map_task(settings.data, mapper, combiner);
        } else {
        }
    }
    main();
};
})(jQuery);