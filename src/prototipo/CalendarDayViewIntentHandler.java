package prototipo;
import java.util.Optional;

import org.json.JSONArray;

import com.amazon.ask.dispatcher.request.handler.HandlerInput;
import com.amazon.ask.dispatcher.request.handler.impl.IntentRequestHandler;
import com.amazon.ask.model.Intent;
import com.amazon.ask.model.IntentRequest;
import com.amazon.ask.model.Response;

public class CalendarDayViewIntentHandler implements IntentRequestHandler {
    @Override
    public boolean canHandle(HandlerInput input, IntentRequest intentRequest) {
        return intentRequest.getIntent().getName().equals("CalendarDayViewIntent");
    }

    @Override
    public Optional<Response> handle(HandlerInput input, IntentRequest intentRequest) {
        WebServiceProtoype wsp = new WebServiceProtoype();
        String response = "";
        wsp.getToken("student", "moodle");
        JSONArray jsonarray = wsp.getCalendayDayView(2019, 12, 12).getJSONArray("events");
		int size = jsonarray.length();
		for (int i = 0; i < size; i++) {
			response += "\nLa actividad ";
			response += jsonarray.getJSONObject(i).getString("name");
			response += " termina el ";
			response += jsonarray.getJSONObject(i).getString("formattedtime").replaceAll("<.*?>", "");
		}

        Intent intent = intentRequest.getIntent();
        String intentName = intent.getName();

        return input.getResponseBuilder()
                .withSpeech(response)
                .build();
    }
}
