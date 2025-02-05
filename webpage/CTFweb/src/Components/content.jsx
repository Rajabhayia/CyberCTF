import React, { useState } from "react";
import './Nav.css'

import Topics from "./Topics/topics";

function Content() {

  return (
    <div className="contentData">
      <Topics/>
    </div>
  );
}

export default Content;
