/* Contains code to render the view of the admin panel */
import React from 'react';
import Axios from 'axios';
import ReactTable from "react-table";
import 'react-table/react-table.css'
import 'regenerator-runtime/runtime';

/**
 * AdminPage is the "administrative interface" of the app
 */
class AdminPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tokens: [],
            loading: true,
            totalPages: 0,
        }
        this.pageSize = 25;
        this.getData = this.getData.bind(this);
    }

    /**
     * getData fetches a page full of tokens and their frequencies
     * from the backend, and stores it in the state of this component
     * @param {*} state The state of ReactTable
     * @param {*} _ 
     */
    async getData(state, _) {
        const params = {
            // page: state.page * this.pageSize,
            page: state.page,
            size: this.pageSize,
        }
        this.setState({ loading: true });

        let response;
        try {
            response = await Axios.get('/tokens', { params: params });
        } catch (err) {
            console.error(err)
            return
        }
        this.setState({
            tokens: response.data.tokens,
            totalPages: Math.ceil(response.data.total / this.pageSize),
            loading: false,
        });
    }

    /**
     * createTable renders a ReactTable to list tokens with their frequencies
     */
    createTable() {
        const { tokens, loading, totalPages } = this.state;
        return (
            <ReactTable
                data={tokens}
                columns={[
                    {
                        Header: "Token",
                        accessor: "token",
                    },
                    {
                        Header: "Frequency",
                        accessor: "frequency"
                    }
                ]}
                manual={true}
                pages={totalPages}
                loading={loading}
                showPageSizeOptions={false}
                onFetchData={this.getData}
                filterable={false}
                sortable={false}
                className='-striped -highlight'
            />
        )
    }

    render() {
        return (
            <div>
                {this.createTable()}
            </div>
        )
    }
}

export default AdminPage;