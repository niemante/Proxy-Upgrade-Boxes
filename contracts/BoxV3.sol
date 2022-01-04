// SPDX-License-Identifier: MIT
// # export NODE_OPTIONS=--openssl-legacy-provider

pragma solidity ^0.8.0;

contract BoxV3 {
    uint private value;

    event ValueChanged(uint256 newValue);

    function store(uint256 newValue) public {
        value = newValue;
        emit ValueChanged(value);
    }
     
    function retrieve() public view returns(uint256) {
        return value;
    } 

    function multiply_10() public {
        value = value * 10;
        emit ValueChanged(value);
    }

}    