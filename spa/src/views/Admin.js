import React from 'react';
import Axios from 'axios';
import ReactTable from "react-table";
import 'react-table/react-table.css';


class AdminPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tokens = [],
        }
    }

    render(){
        return(
            <div>
                <ReactTable
                    data={this.props.tokens}
                    columns = {[
                        {
                            Header: "Token",
                            accessor: "token",
                        },
                        {
                            Header: "Frequency",
                            accessor: "frequency"
                        }
                    ]}
                />
            </div>
        )
    }
}