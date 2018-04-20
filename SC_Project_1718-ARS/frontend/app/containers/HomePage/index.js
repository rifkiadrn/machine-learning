/*
 * HomePage
 *
 * This is the first thing users see of our App, at the '/' route
 *
 * NOTE: while this component should technically be a stateless functional
 * component (SFC), hot reloading does not currently support SFCs. If hot
 * reloading is not a necessity for you then you can refactor it and remove
 * the linting exception.
 */

import React from 'react';
import styled from 'styled-components';
import Hero from 'components/Hero/Loadable';
import FaSearch from 'react-icons/lib/fa/search';
import FaList from 'react-icons/lib/fa/list';
import FaStar from 'react-icons/lib/fa/star';
import FaHistory from 'react-icons/lib/fa/history';

export default class HomePage extends React.PureComponent { // eslint-disable-line react/prefer-stateless-function
  render() {
    const StyledSection = styled.div`
      height: 100vh;
      background-color: #2B2D42;
    `;

    const Footer = () => {

    };
    return (
      <div>
        <Hero noBottomLine/>
        <div className="container" >
          <div className="row">
            <div className="col-md-3"></div>
            <div className="col-md-3">
              <div className="container">
                <div className="icon"><span><FaSearch /></span></div>
                <div className="content">Search any movies as you like. We have over 1000+ movies in our database.</div>
              </div>
              <div className="container">
                <div className="icon"><span><FaList/></span></div>
                <div className="content">Get detailed information about your favorite movies. Get the movie plot , list of actors and many more.</div>
              </div>
            </div>
            <div className="col-md-3">
              <div className="container">
                <div className="icon"><span><FaStar /></span></div>
                <div className="content">Predict the rating of your favorite movies. You can compare the actual rating and predicted rating or you can predict movies that have not released yet.</div>
              </div>
              <div className="container">
                <div className="icon"><span><FaHistory /></span></div>
                <div className="content">Keeps your prediction of a movie. You can show it to your friend or colleague.</div>
              </div>
            </div>
          </div>
        </div>
        <StyledSection>a</StyledSection>
      </div>
    );
  }
}
