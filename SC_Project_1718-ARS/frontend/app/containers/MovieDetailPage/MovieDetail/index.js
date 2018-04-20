/**
 *
 * MovieDetail
 *
 */

import React from 'react';
import styled from 'styled-components';
import { Helmet } from 'react-helmet';
import Vibrant from 'node-vibrant';
import get from 'lodash/get';
import FaStar from 'react-icons/lib/fa/star';
import FaStarOutline from 'react-icons/lib/fa/star-o';

import Hero from 'components/Hero/Loadable';
import LoadingIndicator from 'components/LoadingIndicator';

class MovieDetail extends React.Component {
  // eslint-disable-line react/prefer-stateless-function
  setupColor(movie) {
    if (movie) {
      Vibrant.from(movie.images.thumbnail).getPalette((err, palette) => {
        if (!palette) {
          return;
        }
        const check = this.swatches;
        this.swatches = palette;
        !check && this.forceUpdate();
      });
      if (this.swatches) {
        const arr = Object.keys(this.swatches);
        let respItem = {};
        arr.map(colorName => {
          let temp = get(this.swatches, colorName, {
            getHex: () => 'white',
          });
          if (!temp) {
            temp = {
              getHex: () => 'white',
            };
          }
          respItem[`${colorName}Color`] = temp.getHex();
        });
        return respItem;
      }
    }
    return {};
  }

  render() {
    const { movie, onPredictMovie, moviedetailpage } = this.props;
    const { loadingPredict, prediction } = moviedetailpage;
    const { VibrantColor, LightMutedColor } = this.setupColor(movie);
    const MovieDiv = styled.div`
      background-color: rgba(0, 0, 0, 0.5);
      color: ${LightMutedColor};
      padding-left: 0;
      border-radius: 0.5em;
      overflow: hidden;

      & .details {
        padding-top: 1em;
        padding-bottom: 1em;
      }

      & .genre {
        text-transform: uppercase;
        font-weight: bold;
      }

      & .title {
        color: ${VibrantColor};
        text-transform: uppercase;
        font-weight: bold;
      }

      & .description {
        color: white;
      }

      & .actors {
        color: ${VibrantColor};
        text-transform: uppercase;
      }

      & .duration {
        text-transform: uppercase;
        color: white;
        font-weight: bold;
      }

      & .predicted-rating {
        color: yellow;
      }

      & .actual-rating {
        color: greenyellow;
      }
    `;

    const Footer = () => (
      <MovieDiv className="container">
        <div className="row">
          <div className="col-5">
            <img
              className="img img-fluid"
              src={movie && movie.images.full}
              alt="movie image"
            />
          </div>
          {movie ? (
            <div className="col details">
              <div className="row">
                <div className="col-12 genre align-right justify-content-end small text-right my-2">
                  {movie && movie.genre.join(', ')}
                </div>
                <h1 className="col-12 title my-5">{movie && movie.title}</h1>
                <div className="col-12 description">{movie && movie.plot}</div>
                <div className="col-12 actors my-3">
                  {movie && movie.actors.join(', ')}
                </div>
                <div className="col-12 duration">
                  RUNNING TIME: {movie && movie.duration} MIN
                </div>
                <div className="col-12 my-3">
                  {prediction && (
                    <div className="row text-center">
                      <div className="col-6">
                        <div className="col-12">Actual Rating</div>
                        <h3 className="col-12 actual-rating">
                          {prediction.actual_rating}
                        </h3>
                      </div>
                      <div className="col-6">
                        <div className="col-12">Predicted Rating</div>
                        <h3 className="col-12 predicted-rating">
                          {prediction.rating_predicted}
                        </h3>
                      </div>
                    </div>
                  )}
                </div>
                {loadingPredict ? (
                  <LoadingIndicator />
                ) : (
                  <div className="col-12 mt-2 text-center">
                    <button
                      onClick={onPredictMovie}
                      className="btn btn-outline-warning btn-lg"
                      disabled={!!prediction}
                    >
                      {prediction
                        ? `Elapsed time ${prediction.time_elapsed} second(s)`
                        : 'Predict Now'}
                    </button>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="col">
              <LoadingIndicator />
            </div>
          )}
        </div>
      </MovieDiv>
    );
    return (
      <div>
        <Helmet>
          <title>MovieDetailPage</title>
          <meta name="description" content="Description of MovieDetailPage" />
        </Helmet>
        <article>
          <section id="hero">
            <Hero
              hideLogo
              noBottomLine
              backgroundImage={movie && movie.images.thumbnail}
              footer={<Footer />}
            />
          </section>
        </article>
      </div>
    );
  }
}

MovieDetail.propTypes = {};

export default MovieDetail;
