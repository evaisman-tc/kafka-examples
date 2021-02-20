package com.tucows;

import io.smallrye.common.constraint.NotNull;
import org.eclipse.microprofile.reactive.messaging.Incoming;
import org.jboss.logging.Logger;
import com.tucows.avro.Movie;

import javax.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class MovieConsumer {

    private static final Logger LOGGER =
            Logger.getLogger("MovieConsumer");

    @Incoming("movies-from-kafka")
    @NotNull
    public void receive(Movie movie) {
        LOGGER.infof("Received movie: %s (%d)",
                movie.getTitle(), movie.getYear());
    }

}