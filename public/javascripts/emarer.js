(function(jQuery) {
jQuery.fn.emarer = function(settings) {

    settings = jQuery.extend({
        mapper:     'null',
        combiner:   'null',
        reducer:    'null',
        
        max_emitted: 1000,
        context:    'local',
    }, settings);
    
    ////////////////////////////////////////////////////////////////////////////
    // Fields
    var _emitted = [];
    var _num_emitted = 0;
    
    ////////////////////////////////////////////////////////////////////////////
    // Public Methods
    
    /*
     * Emits a Key/Value(s) pair from a locally execution function.  This
     * function's implementation has nothing to do with push results back to the
     * main server -- it simply appends results to a local array.
     *
     * This function will flush itself once it is either done processing, or has
     * reached `settings.max_emitted`.  Refer to `_flush_emitted` for more
     * documentation on this process.
     */
    function emit(key, value) {
        _emitted.push([key, value]);
        _num_emitted += 1;
        
        if(_num_emitted >= settings.max_emitted) {
            _flush_emitted();
        }
    }
    
    ////////////////////////////////////////////////////////////////////////////
    // Private Methods
    
    /*
     * For a given (key,value) pair, emit the same pair.  Useful for functions
     * which aren't implemented.
     */
    function _null_func(key, value) {
        emit(key, value);
    }
    
    /*
     * Pushes current `_emitted` values back to the master server.  This method
     * will not schedule itself, and should be managed by some other function.
     * At the moment, this is the `emit` function reaching a boundry (likely
     * `settings.max_emitted).  Consult that function for further information.
     */
    function _flush_emitted() {
        var emit_values = new Object();
        
        jQuery.each(_emitted, function(i, kv) {
            var key = kv[0];
            var val = kv[1];
            
            if(!emit_values[key]) {
                emit_values[key] = [val];
            } else {
                emit_values[key].push(val);
            }
        });
        
        console.log("Emitting", emit_values);
        _reset_emitted();
    }
    
    /*
     * Reset all emitted key/value pairs since either instantiation or the last
     * call to this function.  This makes no attempt to store or maintain the
     * current state, it simply resets it.
     */
    function _reset_emitted() {
        _emitted = [];
        _num_emitted = 0;
    }
    
    
    function _fetch_resource() {
        var data;
        
        $.ajax({
            type:       'GET',
            url:        settings.resource,
            async:      false,
            success:    function(response_data) {
                data = response_data;
            }
        });
        
        return data;
    }
    
    function _perform_map(map_func, lines) {
        _reset_emitted();
        
        jQuery.each(lines, function(i, line) {
            map_func(null, jQuery.trim(line));
        });
    }
    
    function _perform_reduce(reduce_func, emitted_key_vals) {
        _reset_emitted();
        
        var key_vals = new Object();
        jQuery.each(emitted_key_vals, function(i, kv) {
            var key = kv[0];
            var val = kv[1];
            
            if(!key_vals[key]) {
                key_vals[key] = [];
            }
            key_vals[key].push(val);
        });
        
        jQuery.each(key_vals, function(key, values) {
           reduce_func(key, values);
        });
    }
    
    function _display_emitted() {
        jQuery.each(_emitted, function(i, emitted) {
            var key = emitted[0];
            var val = emitted[1];
            
            console.log(key, ' = ', val);
        });
    }
    
    function _clone_array(arr) {
        var new_array = []
        jQuery.each(arr, function(i, el) { new_array.push(el); });
        return new_array;
    }
    
    ////////////////////////////////////////////////////////////////////////////
    // Main
    
    function main() {
        var data = _fetch_resource();
        var lines = data.split('\n');
        var map_func, red_func;
        
        eval("map_func = " + settings.mapper);
        eval("com_func = " + settings.combiner);
        eval("red_func = " + settings.reducer);
        
        if(map_func) {
            _perform_map(map_func, lines);
        }
        
        if(red_func) {
            _perform_reduce(red_func, _clone_array(_emitted));
        }
    }
    main();
};
})(jQuery);