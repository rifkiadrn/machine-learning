/**
 *
 * MovieItem
 *
 */

import React from 'react';
import styled from 'styled-components';
import {Link} from 'react-router-dom';
import {FaAngleRight} from 'react-icons/lib/fa';


class MovieItem extends React.Component { // eslint-disable-line react/prefer-stateless-function
  render() {
    const Wrapper = styled.div`
      background: white;
      margin-top: 1em;
      margin-bottom: 1em;
      -webkit-box-shadow: 0 0.2em 0.5em 0 rgba(0,0,0,0.39) ;
      box-shadow: 0 0.2em 0.5em 0 rgba(0,0,0,0.39) ;
      -webkit-transition: all 200ms cubic-bezier(0.19, 1, 0.22, 1) 10ms;
      -moz-transition: all 200ms cubic-bezier(0.19, 1, 0.22, 1) 10ms;
      -o-transition: all 200ms cubic-bezier(0.19, 1, 0.22, 1) 10ms;
      transition: all 200ms cubic-bezier(0.19, 1, 0.22, 1) 10ms;
      
      &:hover {
        -webkit-box-shadow: 0 0.875em 0.938em -0.625em rgba(0,0,0,0.39) ;
        box-shadow: 0 0.875em 0.938em -0.625em rgba(0,0,0,0.39) ;
        -webkit-transform:   translateY(-0.313em) ;
        transform:   translateY(-0.313em) ;
      }
      
      &:active {
        -webkit-box-shadow: none;
        box-shadow: none;
        -webkit-transform: none;
        transform: none;
      }
      
      & .title {
        font-size: 2em;
      }
      
      & .subtitle {
        font-size: .75em;
        color: #D90429;
      }
      
      & img {
        height: 8em;
        width: auto;
        border: 2px solid #8D99AE;
      }
    `;

    const StyledLink = styled(Link)`
      color: rgba(0,0,0,0.58);

      &:hover {
        opacity: 1;
        color: #000;
      }
      
      &, &:hover{
        text-decoration: none;
      }
      
      & .predicted-rating {
        color: red;
      }

      & .actual-rating {
        color: grey;
      }
    `;
    const {Title, Year, imdbID, Type, Poster, rating} = this.props.data;
    return (
      <StyledLink to={rating ? '#' : `/movie/${imdbID}`}>
        <Wrapper className="container">
          <div className="media">
            <img className="mr-3" src={Poster} alt="name"/>
            <div className="media-body align-self-center">
              <div className="row">
                <div className="col">
                  <h5 className="mt-0 title">{Title}</h5>
                  <span className="subtitle">{Year}</span>
                </div>
                <div className="col-auto align-self-center mr-4 text-center">
                  {
                    rating ? (
                      <div>
                        <div className="col-12">Actual Rating</div>
                        <div className="col-12 actual-rating"><h3>{rating.actual}</h3></div>
                        <div className="col-12">Predicted Rating</div>
                        <div className="col-12 predicted-rating"><h3>{rating.predicted}</h3></div>
                      </div>
                    ): <FaAngleRight size={64} color="8D99AE"/>
                  }

                </div>
              </div>
            </div>
          </div>
        </Wrapper>
      </StyledLink>
    );
  }
}

MovieItem.propTypes = {};

export default MovieItem;
