/**
*
* SearchBar
*
*/

import React from 'react';
import PropType from 'prop-types';
import {debounce} from 'lodash';
// import styled from 'styled-components';


class SearchBar extends React.PureComponent { // eslint-disable-line react/prefer-stateless-function
  constructor(props) {
    super(props);

    this.onChangeSearchText = this.onChangeSearchText.bind(this);
    this.moveCaretAtEnd = this.moveCaretAtEnd.bind(this);
    this.onSearchClick = this.onSearchClick.bind(this);
    this.onChangeDebounce = debounce(value => this.props.onChangeSearchText(value), 800);
  }

  onChangeSearchText(e) {
    this.onChangeDebounce(e.target.value);
  }

  onSearchClick() {
    this.onChangeDebounce(this.props.text);
  }

  moveCaretAtEnd(e) {
    let temp_value = e.target.value;
    e.target.value = '';
    e.target.value = temp_value
  }

  render() {
    return (
      <div className="row">
        <div className="col">
          <input ref={(input) => this.input = input} type="text" className="form-control" placeholder="Title or Genre" autoFocus onFocus={this.moveCaretAtEnd} onChange={this.onChangeSearchText} defaultValue={this.props.text}/>
        </div>
        <div className="col-auto">
          <button className="btn btn-danger" type="button" onClick={this.onSearchClick}>SEARCH</button>
        </div>
      </div>
    );
  }
}

SearchBar.propTypes = {
  text: PropType.string,
  onSearchClick: PropType.func,
  onChangeSearchText: PropType.func,
};

SearchBar.defaultProps = {
  text: "",
  onSearchClick: null,
  onChangeSearchText: null,
};

export default SearchBar;
