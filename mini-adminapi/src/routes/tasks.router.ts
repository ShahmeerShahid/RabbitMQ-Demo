import { Router } from "express";

const router = Router();

router.route("/").post(async (req, res) => {
	const body = req.body;
	const rabbitmqChannel = await req.rabbitmqChannelPromise;
	rabbitmqChannel.sendToQueue("tasks", Buffer.from(JSON.stringify(body)));
	res.json({ message: "Task published" });
});

export default router;
