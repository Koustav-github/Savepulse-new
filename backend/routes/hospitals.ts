import { Router } from "express";
import { findHospitalsInRadius } from "../services/hospitalService";

const router = Router();

router.get("/", async (req, res) => {
  const { lat, lng, radius } = req.query;

  if (!lat || !lng) {
    return res.status(400).json({ error: "Latitude (lat) and Longitude (lng) query parameters are required" });
  }

  try {
    const latitude = parseFloat(lat as string);
    const longitude = parseFloat(lng as string);
    const radiusKm = radius ? parseFloat(radius as string) : 10;

    if (isNaN(latitude) || isNaN(longitude)) {
      return res.status(400).json({ error: "Invalid latitude or longitude" });
    }

    const nearbyHospitals = await findHospitalsInRadius({ latitude, longitude }, radiusKm);

    res.json({
      success: true,
      hospitals: nearbyHospitals,
      count: nearbyHospitals.length
    });
  } catch (error) {
    console.error("Hospitals API Error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

export default router;
