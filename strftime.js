/* strftime for JavaScript 

   Field description (taken from http://tinyurl.com/65s2qw)

    %a 	Locale’s abbreviated weekday name. 	 
    %A 	Locale’s full weekday name. 	 
    %b 	Locale’s abbreviated month name. 	 
    %B 	Locale’s full month name. 	 
    %c 	Locale’s appropriate date and time representation. 	 
    %d 	Day of the month as a decimal number [01,31]. 	 
    %H 	Hour (24-hour clock) as a decimal number [00,23]. 	 
    %I 	Hour (12-hour clock) as a decimal number [01,12]. 	 
    %j 	Day of the year as a decimal number [001,366]. 	 
    %m 	Month as a decimal number [01,12]. 	 
    %M 	Minute as a decimal number [00,59]. 	 
    %p 	Locale’s equivalent of either AM or PM.
    %S 	Second as a decimal number [00,61].
    %U 	Week number of the year (Sunday as the first day of the week) as a
        decimal number [00,53]. All days in a new year preceding the first
        Sunday are considered to be in week 0.
    %w 	Weekday as a decimal number [0(Sunday),6]. 	 
    %W 	Week number of the year (Monday as the first day of the week) as a
        decimal number [00,53]. All days in a new year preceding the first
        Monday are considered to be in week 0.
    %x 	Locale’s appropriate date representation. 	 
    %X 	Locale’s appropriate time representation. 	 
    %y 	Year without century as a decimal number [00,99]. 	 
    %Y 	Year with century as a decimal number. 	 
    %Z 	Time zone name (no characters if no time zone exists). 	 
    %% 	A literal '%' character.
*/

var days = [ 
    'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
    'Saturday' 
];

var months = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'
];

function shortname(name) {
    return name.substr(0, 3);
}

function zeropad(n, size) {
    n = '' + n; /* Make sure it's a string */
    size = size || 2;
    while (n.length < size) {
        n = '0' + n;
    }
    return n;
}

function twelve(n) {
    return (n <= 12) ? n : 24 - n;
}

function strftime(format, date) {
    date = date || new Date();
    var fields = {
        a: shortname(days[date.getDay()]),
        A: days[date.getDay()],
        b: shortname(months[date.getMonth()]),
        B: months[date.getMonth()],
        c: date.toString(),
        d: zeropad(date.getDate()),
        H: zeropad(date.getHours()),
        I: zeropad(twelve(date.getHours())),
        /* FIXME: j: */
        m: zeropad(date.getMonth() + 1),
        M: zeropad(date.getMinutes()),
        p: (date.getHours() >= 12) ? 'PM' : 'AM',
        S: zeropad(date.getSeconds()),
        w: zeropad(date.getDay() + 1),
        /* FIXME: W: */
        x: date.toLocaleDateString(),
        X: date.toLocaleTimeString(),
        y: ('' + date.getFullYear()).substr(2, 4),
        Y: '' + date.getFullYear(),
        /* FIXME: Z: */
        '%' : '%'
    };

    var result = '', i = 0;
    while (i < format.length) {
        if (format[i] === '%') {
            result = result + fields[format[i + 1]];
            ++i;
        }
        else {
            result = result + format[i];
        }
        ++i;
    }
    return result;
}
