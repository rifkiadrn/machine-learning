/**
*
* TextInput
*
*/

import React from 'react';
import TextInput from 'components/TextInput';
import MdCheck from 'react-icons/lib/md/check';

class Form extends React.PureComponent { // eslint-disable-line react/prefer-stateless-function
  render() {
    return (
      <form>
        <TextInput id="title" name="title" placeholder="Movie name..." label="Title" />
        <TextInput id="movie-url" name="url" placeholder="http:// or https://" label="IMDb URL" />
        <div className="row justify-content-center justify-content-md-end">
          <div className="col-auto">
            <button className="btn btn-danger">
              <MdCheck />
              Send
            </button>
          </div>
        </div>
      </form>
    );
  }
}

Form.propTypes = {

};

export default Form;
