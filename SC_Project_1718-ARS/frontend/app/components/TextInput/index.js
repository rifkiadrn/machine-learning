/**
 *
 * TextInput
 *
 */

import React from 'react';
import PropTypes from 'prop-types';


class TextInput extends React.PureComponent { // eslint-disable-line react/prefer-stateless-function
  render() {
    const { placeholder, id, label, name } = this.props;
    return (
      <div className="form-group">
        <label className="col-form-label" htmlFor={id}>{label}</label>
        <input type="text" name={name} className="form-control" id={id} placeholder={placeholder} />
      </div>
    );
  }
}

TextInput.propTypes = {
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  placeholder: PropTypes.string,
  label: PropTypes.string,
};

TextInput.defaultProps = {
  placeholder: 'Example input',
  label: 'Example Lable',
};

export default TextInput;
