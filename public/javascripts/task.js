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
    
    function _perform_reduce_task(data, reduce_func) {
        var last_key     = null;
        var value_buffer = [];
        
        jQuery.each(data, function(i, key_val) {
            var key = key_val[0];
            var val = key_val[1];
            
            if((last_key != null) && (key != last_key)) {
                reduce_func(last_key, value_buffer);
                
                value_buffer = [];
            }
            
            value_buffer.push(val);
            last_key = key;
        });
        
        if(last_key != null) {
            reduce_func(last_key, value_buffer);
        }
        
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
                return;
            }
            
            try {
                eval("combiner = "+ settings.combiner);
            } catch(e) {
                _compilation_error('Combiner', e);
            }
            
            _perform_map_task(settings.data, mapper, combiner);
            
        } else {
            var reducer = null;
            var data    = settings.data;
            
            try {
                eval("reducer = "+ settings.reducer);
            } catch(e) {
                _compilation_error('Reducer', e);
                return;
            }

            _perform_reduce_task(data, reducer);
        }
    }
    main();
};
})(jQuery);