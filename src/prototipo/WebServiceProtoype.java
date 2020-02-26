package prototipo;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;
import org.jsoup.Jsoup;


public class WebServiceProtoype {
	private String host = "https://school.moodledemo.net";
	private String token;
	private int userid;
	private List<Integer> courseids = new ArrayList<Integer>();
	
	public void setHost(String host) {
		this.host = host;
	}

	public void getToken(String username, String password) {
		String url = host + "/login/token.php?username=" + username + "&password=" + password + "&service=moodle_mobile_app";
		try {
			String contenido = Jsoup.connect(url).ignoreContentType(true).execute().body();
			JSONObject jsonObject = new JSONObject(contenido);
			token = jsonObject.getString("token");
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void getUserID() {
		String url = host + "/webservice/rest/server.php?wstoken=" + token + "&moodlewsrestformat=json&wsfunction=core_webservice_get_site_info";
		try {
			String contenido = Jsoup.connect(url).ignoreContentType(true).execute().body();
			JSONObject jsonObject = new JSONObject(contenido);
			userid = jsonObject.getInt("userid");
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public JSONObject getCalendayDayView(int year, int month, int day) {
		String url = host + "/webservice/rest/server.php?wstoken=" + token + "&moodlewsrestformat=json&wsfunction=core_calendar_get_calendar_day_view&year="
				+ year + "&month=" + month +"&day=" + day;
		JSONObject jsonobject = null;
		try {
			String contenido = Jsoup.connect(url).ignoreContentType(true).execute().body();
			jsonobject = new JSONObject(contenido);
		} catch (IOException e) {
			e.printStackTrace();
		}
		return jsonobject;
	}
	
	public JSONObject getCalendarEventsByCourseID(int courseid) {
		String url = host + "/webservice/rest/server.php?wstoken=" + token + "&moodlewsrestformat=json&wsfunction=core_calendar_get_action_events_by_course&courseid="
				+ courseid;
		JSONObject jsonObject = null;
		try {
			String contenido = Jsoup.connect(url).ignoreContentType(true).execute().body();
			jsonObject = new JSONObject(contenido);
		} catch (IOException e) {
			e.printStackTrace();
		}
		return jsonObject;
	}
	
	public JSONObject getUsersCourses(int userid) {
		String url = host + "/webservice/rest/server.php?wstoken=" + token + "&moodlewsrestformat=json&wsfunction=core_enrol_get_users_courses&userid="
				+ userid;
		JSONObject jsonObject = null;
		try {
			String contenido = Jsoup.connect(url).ignoreContentType(true).execute().body();
			jsonObject = new JSONObject(contenido);
		} catch (IOException e) {
			e.printStackTrace();
		}
		return jsonObject;
	}
	
	public static void main(String[] args) {
		WebServiceProtoype wsp = new WebServiceProtoype();
		//wsp.setHost("https://school.moodledemo.net");
		wsp.getToken("student", "moodle");
		JSONArray jsonarray = wsp.getCalendayDayView(2019, 12, 12).getJSONArray("events");
		int size = jsonarray.length();
		for (int i = 0; i < size; i++) {
			System.out.print("\nNombre: " + jsonarray.getJSONObject(i).getString("name"));
			System.out.print("\nFecha y hora: " + jsonarray.getJSONObject(i).getString("formattedtime").replaceAll("<.*?>", ""));
		}
	}
}
