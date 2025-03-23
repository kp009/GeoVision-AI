import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const ImageUpdatePage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [imageData, setImageData] = useState({ location: "", latitude: "", longitude: "" });

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/image-location/${id}/`)
      .then((res) => res.json())
      .then((data) => setImageData(data))
      .catch((err) => console.error(err));
  }, [id]);

  const handleUpdate = async () => {
    await fetch(`http://127.0.0.1:8000/api/image-location/${id}/update/`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(imageData),
    });
    navigate("/"); // Redirect after update
  };

  return (
    <div>
      <h2>Edit Image Location</h2>
      <input type="text" value={imageData.location} onChange={(e) => setImageData({ ...imageData, location: e.target.value })} />
      <input type="text" value={imageData.latitude} onChange={(e) => setImageData({ ...imageData, latitude: e.target.value })} />
      <input type="text" value={imageData.longitude} onChange={(e) => setImageData({ ...imageData, longitude: e.target.value })} />
      <button onClick={handleUpdate}>Update</button>
    </div>
  );
};

export default ImageUpdatePage;
