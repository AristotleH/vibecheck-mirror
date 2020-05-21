import _ from "lodash";
import React from "react";
import ReactDOM from "react-dom";

import { Menu, Grid, Search } from "semantic-ui-react";

import "./index.css";
import "semantic-ui-css/semantic.min.css";

const initialSearchState = { 
    isLoading: false, 
    results: [], 
    value: "", 
    timeout: 0,
};

const initialMenuState = { 
    activeItem: "search",
};

class SearchPage extends React.Component {
    render() {
        return (
            <div>
                <HeaderMenu />
                <ContentSearch />
            </div>
        );
    }
}

class HeaderMenu extends React.Component {
    constructor(props) {
        super(props);
        this.state = initialMenuState
    }

    handleItemClick = (e, { name }) => this.setState({ activeItem: name });

    render() {
        const { activeItem } = this.state;
        return (
            <Menu>
                <Menu.Item
                    name="search"
                    active={activeItem === "search"}
                    onClick={this.handleItemClick}
                >
                    Search
                </Menu.Item>

                <Menu.Item
                    name="trends"
                    active={activeItem === "trends"}
                    onClick={this.handleItemClick}
                >
                    Trends
                </Menu.Item>
            </Menu>
        );
    }
}

class ContentSearch extends React.Component {
    constructor(props) {
        super(props);
        this.state = initialSearchState
        this.state.avg_sentiment = "(mean sentiment score, (-1 to 1 inclusive)"
        this.state.sentiment_string = "TBD"
    }

    handleSearchChange = (e, { value }) => {
        this.setState({ isLoading: true, value });

        if(this.timeout) 
            clearTimeout(this.timeout);

        this.timeout = setTimeout(() => {
            if (this.state.value.length < 1) 
                return this.setState(initialSearchState);

            this.getData(value)

            this.setState({
                isLoading: false,
            });
        }, 1500);
    };

    render() {
        return (
            <Grid container>
                <Grid.Row centered style={{ padding: "150pt 0 0 0" }}>
                    <div className="logo">vibecheck</div>
                </Grid.Row>
                <Grid.Row centered style={{ padding: "50pt 0 0 0" }}>
                    <Search
                        className="search-bar"
                        loading={ this.state.isLoading }
                        placeholder="what's on your mind?"
                        onSearchChange={_.debounce(
                            this.handleSearchChange,
                            500,
                            { leading: true }
                        )}
                        value={ this.state.value }
                        open={ false }
                        {...this.props}
                    />
                </Grid.Row>
                <Grid.Row centered style={{ padding: "20pt 0 0 0" }}>
                    <div className="header">   
                        {"Sentiment Score: " + this.state.avg_sentiment}
                        </div>
                </Grid.Row>
                <Grid.Row centered style={{ padding: "5pt 0 0 0" }}>
                    <div className="header">
                        {"Vibes: " + this.state.sentiment_string}
                        </div>
                </Grid.Row>
            </Grid>
        );
    }

    getData(search) {
        fetch(`/search/${search}`)
            .then((res) => res.json())
            .then((data) => {
                console.log(data);
                let avg_sent = data.avg_sentiment;//data.avg_sentiment

                let sent_string = "neutral"
                if(avg_sent >= .05) {
                    sent_string = "positive"
                } else if(avg_sent <= -0.05) {
                    sent_string = "negative"
                }
                this.setState({
                    avg_sentiment: avg_sent,
                    sentiment_string: sent_string
                })
            });
    }
}

ReactDOM.render(<SearchPage />, document.getElementById("root"));