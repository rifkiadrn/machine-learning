/**
 *
 * MovieForm
 *
 */

import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { createStructuredSelector } from 'reselect';
import { compose } from 'redux';
import styled from 'styled-components';

import injectReducer from 'utils/injectReducer';
import makeSelectMovieForm from './selectors';
import reducer from './reducer';

import Form from './Form/index';

export class MovieForm extends React.Component { // eslint-disable-line react/prefer-stateless-function
  render() {
    const Wrapper = styled.div`
      background-color: #E6AF2E;
      padding-top: 1em;
      padding-bottom: 1em;
      
      & label {
        color: white;
      }
    `;

    const BorderedDiv = styled.div`
      border-left: 1px dashed red;
     `;
    return (
      <Wrapper className="container-fluid">
        <div className="container">
          <div className="row">
            <div className="col-12 col-md-7 align-self-center text-md-right text-center">
              <div className="row">
                <div className="col">
                  Not Found Your Beloved Movie?
                </div>
              </div>
              <div className="row">
                <div className="col display-2">Tell Us!</div>
              </div>
            </div>
            <BorderedDiv className="col-12 col-md-5">
              <Form />
            </BorderedDiv>
          </div>
        </div>
      </Wrapper>
    );
  }
}

MovieForm.propTypes = {
  dispatch: PropTypes.func.isRequired,
};

const mapStateToProps = createStructuredSelector({
  movieform: makeSelectMovieForm(),
});

function mapDispatchToProps(dispatch) {
  return {
    dispatch,
  };
}

const withConnect = connect(mapStateToProps, mapDispatchToProps);

const withReducer = injectReducer({ key: 'movieForm', reducer });

export default compose(
  withReducer,
  withConnect,
)(MovieForm);
