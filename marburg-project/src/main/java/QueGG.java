
import core.Constants;
import static core.Constants.NAME;
import static core.Constants.NODE_TYPE;
import static core.Constants.OBJECT;
import static core.Constants.PROPERTY;
import utils.CsvToTurtle;
import core.Prefixes;
import core.Relation;
import graphdb.Entity;
import graphdb.Neo4j;
import graphdb.Property;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import static java.lang.System.exit;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;
import lombok.NoArgsConstructor;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import utils.FileFolderUtils;

@NoArgsConstructor
public class QueGG implements Constants {

    //MATCH (n:Painting) RETURN n LIMIT 25;
    // RELATION
    public static void main(String[] args) {
        // Default Neo4j connection info#
        String javaflag = "True";
        Boolean neo4jFlag = true;
        String uri = "bolt://neo4j:7687";
        String user = "neo4j";
        String password = "password";
        String dir = "dataset/german/input/"; // default CSV path
        String menu = CREATE_FROM_STRING; // default action
        String nodeStr = 
                "Gattung / Genre=Bildende Kunst=yellow=\n"
                +"name=Paar=yellow=\n"
                + "Titel=Paar=yellow=\n"
                + "Technik=Öl Gemälde=yellow=\n"
                + "Dimensionen:=151,5x116 cm=yellow=\n"
                + "Kurzbeschreibung=Paar in leichter Draufsicht und grellem Sonnenlicht mit Schattenpartien gezeigt. Beide tragen bunte Kleidung, die Frau in farbenfroher Tracht blickt aus dem Bild heraus, während der Mann mit Hut zu ihr schaut. Das Gemälde ist einem pointillistischen Stil, indem die Pinselschläge an Mosaik erinnern.=yellow=\n"
                + "Motive / Topoi=Exotismus, Buntheit, Hautfarbe=yellow=\n"
                + "Narrative / Diskurse=No data=red=\n"
                + "Historischer Kontext=Ströher ist Meisterschüler in Berlin und macht Reisen nach Frankreich und Spanien=yellow=\n"
                + "Antiziganistische / Stigmatisierende Elemente=No data=red=\n"
                + "Agency=No data=red=\n"
                + "Verknüpfung=No data=red=\n"
                + "Narrativwandel bei Medienwechsel=No data=red=\n"
                + "Rezeptionsweg=No data=red=\n"
                + "Sammlung / Archiv=No data=red=\n"
                + "Provenienz=Möglicherweise nach Skizzen aus Spanien oder dort entstanden.=yellow=\n"
                + "Literatur=Lebenserinnerungen des Malers Friedrich Karl Ströher 1876 - 1925, hrsg. vom Freundeskreises des Werkes Karl Friedrich Ströher und dem Hunsrück-Museum Simmern, Simmern 2004, S. 52=yellow=\n"
                + "Ausstellungen / Aufführungen / Veröffentlichungen=\"Ströher in Spanien\" Simmern, 2023-2024=yellow=\n"
                + "Objekt- oder Werkteil=No data=red=\n"
                + "Rechte / Lizenzen=No data=red=\n"
                + "Digitalisat-Link/Pfad=No data=red=\n"
                + "Metadaten-Status=No data=red=\n"
                + "Erfasst von=No data=red=\n"
                + "Erfassungsdatum=No data=red=\n"
                + "Kommentar / Anmerkung=No data=red=\n"
                + "Versionsgeschichte=No data=red=\n"
                + "nodeType=Painting==";

        // Parse arguments
        // args[0] = menu, args[1] = CSV dir, args[2] = URI, args[3] = user, args[4] = password
        if (args.length >= 1) {
            menu = args[0];
        }
        if (args.length >= 2) {
            dir = args[1];
        }
        if (args.length >= 3) {
            uri = args[2];
        }
        if (args.length >= 4) {
            user = args[3];
        }
        if (args.length >= 5) {
            password = args[4];
        }
        if (args.length >= 6) {
            nodeStr = args[5];
        }
        if (args.length >= 7) {
            javaflag = args[6];
        }

        if (javaflag.contains("True")) {
            uri = "bolt://localhost:7687";
        } else {
            uri = "bolt://neo4j:7687";
        }

        System.out.println("successfully get inside the java code:");
        System.out.println(menu);
        System.out.println(nodeStr);
        System.out.println(dir + " " + uri + " " + user + " " + password);

        Neo4j app = new Neo4j(uri, user, password);

        if (menu.contains(CREATE)) {
            if (menu.contains(CREATE_FROM_FILE)) {
                List<String> files = FileFolderUtils.getSpecificFiles(dir, "entity", ".csv");
                LinkedHashMap<String, Entity> titles = nodeFromFile(files);
                for (String title : titles.keySet()) {
                    addDataToNeo4j(titles.get(title), neo4jFlag, app);
                }
            }

            if (menu.contains(CREATE_FROM_STRING)) {
                LinkedHashMap<String, String> properties = findPropertiesFromString(nodeStr);
                //System.out.println(properties);
                Entity entity = new Entity(properties);
                addDataToNeo4j(entity, neo4jFlag, app);
            }

        }

        /*if (menu.contains(RELATION)) {
            app.createRelationship(Entity.OBJECT_ID, "Book_1", "Painting_2", "containsPainting");
        }*/
        if (menu.contains(DELETE)) {
            app.deleteAll();
        }
        if (menu.contains(CHECK)) {
            app.listNodes();
        }

    }

    private static void addDataToNeo4j(Entity entity, Boolean neo4jFlag, Neo4j app) {
        System.out.println("entity:" + entity);
        if (neo4jFlag) {
            app.createNodeWithProperties(entity);
        }
        if (entity.getRelation().isRelationExisit()) {
            System.out.println(entity.getRelation());
            if (neo4jFlag) {
                app.createRelationship(entity);
            }
        } else {
            System.out.println(entity.getObjectID() + " No relation found!!");
        }
    }

    private static LinkedHashMap<String, Entity> nodeFromFile(List<String> files) {

        LinkedHashMap<String, Entity> titles = new LinkedHashMap<String, Entity>();
        for (String csvPath : files) {
            if (csvPath.contains(".~lock.")) {
                continue;
            }
            try {
                FileReader reader = new FileReader(Paths.get(csvPath).toFile());
                System.out.println(Paths.get(csvPath).toFile());
                CSVParser csvParser = new CSVParser(reader, CSVFormat.DEFAULT.withFirstRecordAsHeader());
                LinkedHashMap<String, String> properties = new LinkedHashMap<String, String>();
                for (CSVRecord record : csvParser) {
                    Property property = new Property(record.get(PROPERTY), record.get(OBJECT));
                    properties.put(property.getProperty(), property.getObject());
                }
                Entity entity = new Entity(properties);
                titles.put(entity.getSubject(), entity);

            } catch (FileNotFoundException ex) {
                Logger.getLogger(Entity.class.getName()).log(Level.SEVERE, null, ex);
            } catch (IOException ex) {
                Logger.getLogger(Entity.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        return titles;

    }

    private static LinkedHashMap<String, String> findPropertiesFromString(String nodeStr) {
        LinkedHashMap<String, String> properties = new LinkedHashMap<String, String>();
        String[] lines = nodeStr.split("\n");
        for (String line : lines) {
            if (line.contains("=")) {
                String[] info = line.split("\\=");
                if (info.length < 2)
                ; else if (info.length < 4) {
                    System.out.println(line);
                    String att = info[0];
                    att=att.replace(" ", "_");
                    String value = info[1];
                    System.out.println("property >> " + att + " value >> " + value);
                    properties.put(att, value);
                    String att_status = "Z_"+att  ;
                    if (att.contains("nodeType"))
                        ; else {
                        String value_status = info[2];
                        System.out.println("att_status >> " + att_status + " att_status >> " + value_status);
                        properties.put(att_status, value_status);
                    }
                }

            }

        }
        return properties;
    }

}
