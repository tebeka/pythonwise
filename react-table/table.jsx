var Table = React.createClass({
    componentDidMount: function() {
        var table = this;
        $('#load').click(function() {
            $.ajax({
                url: '/data?last=' + table.state.values.length,
                dataType: 'json',
                success: function(objs) {
                    var values = table.state.values.concat(objs);
                    table.setState({values: values});
                }
            });
        });
    },
    getInitialState: function() {
        return {values: []};
    },
    render: function() {
        var rows = this.state.values.map(function(obj) {
            return (
                <tr>
                    <td>{obj.name}</td>
                    <td>{obj.color}</td>
                </tr>
            );
        });

        return (
            <table className="table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Color</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        );
    }
});

function on_ready() {
    React.render(
        <Table />,
        $('#content')[0]
    );
}

$(on_ready);
