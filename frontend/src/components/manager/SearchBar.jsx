import React, { useState } from "react";
import { TextField, Box } from "@mui/material";

const SearchBar = ({ onSearch }) => {
  const [searchQuery, setSearchQuery] = useState("");

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
    onSearch(e.target.value); 
  };

  return (
    <Box mb={4}>
      <TextField
        label="Search by ID"
        variant="outlined"
        fullWidth
        value={searchQuery}
        onChange={handleSearchChange}
        placeholder="Enter employee ID"
      />
    </Box>
  );
};

export default SearchBar;
